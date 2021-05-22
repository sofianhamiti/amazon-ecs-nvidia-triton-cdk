from aws_cdk import (
    aws_iam as iam,
    core
)


class IamStack(core.NestedStack):
    def __init__(self, scope, id) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ================== IAM ROLE ======================
        # ==================================================
        self.role = iam.Role(
            scope=self,
            id='role',
            assumed_by=iam.ServicePrincipal(service='ecs-tasks.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonECS_FullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
            ]
        )
