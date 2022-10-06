import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ecs_patterns from "aws-cdk-lib/aws-ecs-patterns";


export class AppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const vpc = new ec2.Vpc(this, "AppVPC", {
      maxAzs: 3
    });

    const cluster = new ecs.Cluster(this, "CLIWorkshopCluster", {
      vpc: vpc
    });

    // Create a load-balanced Fargate service and make it public
    const service = new ecs_patterns.ApplicationLoadBalancedFargateService(this, "AWSCLIWorkshopDemoApp", {
      cluster: cluster,
      cpu: 512,
      desiredCount: 2,
      taskImageOptions: {
        image: ecs.ContainerImage.fromAsset('../src'),
        containerPort: 5000,
	environment: {
          'MYAPP_FOO': 'BAR',
	},
      },
      memoryLimitMiB: 2048,
      publicLoadBalancer: true,
    });
    service.targetGroup.setAttribute('deregistration_delay.timeout_seconds', '10')
    service.targetGroup.configureHealthCheck({
      interval: cdk.Duration.seconds(5),
      healthyHttpCodes: '200',
      healthyThresholdCount: 2,
      unhealthyThresholdCount: 3,
      timeout: cdk.Duration.seconds(4),
    });
  }
}
