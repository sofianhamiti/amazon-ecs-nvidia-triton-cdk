from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    core
)


class EcsStack(core.NestedStack):
    def __init__(
            self,
            scope,
            id,
            *,
            name=None,
            role=None,
            directory=None,
            vpc=None,
            model_repository=None,
            instance_type=None,
            gpu_count=None
    ) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ================== ECR IMAGE =====================
        # ==================================================
        ecr_image = ecs.ContainerImage.from_asset(directory=directory)

        # ==================================================
        # =============== FARGATE SERVICE ==================
        # ==================================================

        # CREATE CLUSTER
        cluster = ecs.Cluster(scope=self, id='CLUSTER', cluster_name=name, vpc=vpc)

        # USE GPU AMI
        machine_image = ecs.EcsOptimizedImage.amazon_linux2(hardware_type=ecs.AmiHardwareType.GPU)

        cluster.add_capacity(
            id='capacity',
            instance_type=ec2.InstanceType(instance_type),
            machine_image=machine_image,
            cooldown=core.Duration.seconds(600)
        )

        # TASK DEFINITION WITH TRITON CONTAINER
        task_definition = ecs.Ec2TaskDefinition(
            scope=self,
            id='taskdef',
            task_role=role
        )

        container = task_definition.add_container(
            id='Container',
            image=ecr_image,
            command=['/tmp/run.sh'],
            environment={
                'AWS_ROLE_ARN': role.role_arn,
                'MODEL_REPOSITORY': model_repository
            },
            memory_limit_mib=24000,
            gpu_count=gpu_count,
            logging=ecs.LogDriver.aws_logs(stream_prefix='triton')
        )

        container.add_port_mappings(ecs.PortMapping(container_port=8000, host_port=8000, protocol=ecs.Protocol.TCP))
        container.add_port_mappings(ecs.PortMapping(container_port=8001, host_port=8001, protocol=ecs.Protocol.TCP))
        container.add_port_mappings(ecs.PortMapping(container_port=8002, host_port=8002, protocol=ecs.Protocol.TCP))

        self.ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(
            scope=self,
            id="Service",
            cluster=cluster,
            task_definition=task_definition
        )

        # SET CUSTOM PING FOR TRITONSERVER
        self.ecs_service.target_group.configure_health_check(path='/v2/health/ready')

        # SET SECURITY GROUP WITH 8000 FOR HTTP
        self.ecs_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(8000),
            description='Allow inbound from VPC'
        )
