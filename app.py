from aws_cdk import core
from stacks.iam_stack import IamStack
from stacks.vpc_stack import VpcStack
from stacks.ecs_stack import EcsStack


class InferenceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        project_name = 'triton'
        model_repository = '<ADD YOUR S3 MODEL REPOSITORY HERE>'
        instance_type = 'g4dn.2xlarge'
        gpu_count = 1

        # ==================================================
        # ==================== IAM =========================
        # ==================================================
        iam_stack = IamStack(scope=self, id='iam')
        # ==================================================
        # ==================== VPC =========================
        # ==================================================
        vpc_stack = VpcStack(scope=self, id='vpc')

        # ==================================================
        # ============== ECS TRITON SERVER =================
        # ==================================================
        ecs_stack = EcsStack(
            scope=self,
            id='triton',
            name=project_name,
            role=iam_stack.role,
            directory='triton_image',
            model_repository=model_repository,
            vpc=vpc_stack.vpc,
            instance_type=instance_type,
            gpu_count=gpu_count
        )
        # ==================================================
        # =================== OUTPUTS ======================
        # ==================================================
        core.CfnOutput(
            scope=self,
            id='LoadBalancerDNS',
            value=ecs_stack.ecs_service.load_balancer.load_balancer_dns_name
        )


app = core.App()
InferenceStack(app, "TritonStack")
app.synth()
