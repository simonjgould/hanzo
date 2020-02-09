#Hanzo Pipeline

## Assumptions

### A simple branching strategy is used:
* feature branch for any development work including bug fixes
* master branch is the current release candidate (in UAT and staging environments)
* master branch tags are used for releases to the production environment

reasoning: High levels of automation and high test coverage make a more complex branching strategy such as gitflow an
 unnecessary process overhead, adding transaction cost to the release deployments.

### Monorepo used for micro-service:
* All infrastructure, tests, code and configuration for the microservice is contained within the same repository (Github) 

reasoning: Each micro-service is considered to be within a bounded context (Domain Driven Design) and should be treated
 as atomic. as such vertical slices will touch most and sometimes all components and as these change together, they
  should be contained within the same repository. this also reduces complexity and transaction overhead.

### Development, Staging and Production environments are deployed into separate accounts to enforce separation:
* Development account contains:
  * branch specific environments
    * stood up when branch is created
    * torn down once branch merged to master
  * UAT environment: current master branch
  * any contract tests (Pact) and e2e tests can be done in this environment.
* Staging account contains:
  * Staging environment: tagged release candidate on master branch
  * The same data feed as production:
    * so acceptance, security and performance tests can be performed on a production release candidate
* Production account contains:
  * Production environment: tagged release on master branch
    * only basic smoke tests run against this environment
    
### Architecture
* The flask micro-service will be deployed to an AWS container service (ECS fargate or EKS)
* The flask service will be in a private subnet and not publicly accessible.
* The flask service will be independently deploy-able
* Access to the flask service will be managed by either:
  * service mesh
  * private load balancer with static endpoint.
* consumer based contract test will be used to ensure comparability with other component micro-services
* The Redis instance will be deployed into AWS Elastic cache
* The Postgress instance via AWS RDS will have been bootstrapped into each account prior to deployment
  * By prepending the branch name to table creation, this allows for a single AWS RDS to serve all the environments
   within the development account
   
### Build, Testing and deployment requirements
* Unit tests and component integration tests will be run for every build.
* Static analysis and test coverage metrics will be published to a sonarqube instance (Sonarcloud.io)
  * failure to meet the agreed quality gate will fail the build.
* The docker image will be built and pushed to a repository (AWS ECR)
  * the image version will be based on the branch name/tag and the commit id
* the docker image with the appropriate version will be deployed via infrastructure as code to the container service, 
along with any infrastructure changes required.
* Development branch environments and the UAT will allow for e2e and consumer based contract test to be run.
* Once UAT environment has been approved, the master branch will be tagged as a release candidate and the current docker
 images updated with the tag version.
* release candidate tags can be built into the staging environment.
* once a release candidate is built into the staging environment successfully:
  * acceptance, full e2e, performance and security tests can be run.
* On release:
  * the current release candidate tagged commit and docker images are tagged as a release.
  * The release tag and images is deployed
  * basic full e2e smoke tests are run
  
### CI/CD
* the builds run on a Jenkins instance with all appropriate plugins installed and configured:
  * standard plugins
  * pyenv plugin
  * version number plugin
  * docker and python 3.8.1. installed on server
  
### Sonar static analysis
* Extended SonarWay Quality Profile:
  * Added all blockers
  * Added Critical and Major wrt to complexity, file and function size
  
#TODO
## redis
## set up jenk jobs for tags
## try the release stuff