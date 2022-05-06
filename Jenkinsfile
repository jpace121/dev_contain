pipeline {
    agent any

    options
    {
        skipDefaultCheckout(true)
    }
    stages
    {
        stage('Checkout')
        {
          steps
          {
            checkout scm
          }
        }
        stage('Run')
        {
           steps
           {
             sh 'ansible-playbook --skip-tags cleanup,deploy -i inventory.yaml build.yaml'
           }
        }
        stage('Deploy')
        {
            when
            {
               expression
               {
                  currentBuild.result == null || currentBuild.result == 'SUCCESS'
               }
            }
            steps
            {
               sh 'ansible-playbook --tags deploy build.yaml'
            }
        }
    }
    post
    {
        always
        {
            sh 'ansible-playbook --tags cleanup build.yaml'
        }
    }
}
