from aws_cdk import (
    aws_ec2 as ec2,
    core
)


class VpcStack(core.NestedStack):
    def __init__(self, scope, id) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ==================== VPC =========================
        # ==================================================
        self.vpc = ec2.Vpc(
            scope=self,
            id='VPC',
            max_azs=2
        )
        # self.vpc.add_gateway_endpoint('S3Endpoint', service=ec2.GatewayVpcEndpointAwsService.S3)
