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
            cleanWs()
            checkout scm
          }
        }
        stage('Run')
        {
           steps
           {
             sh 'ansible-playbook -vvvv --skip-tags cleanup,deploy -i inventory.yaml build.yaml'
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
               sh 'ansible-playbook --tags deploy -i inventory.yaml build.yaml'
            }
        }
    }
    post
    {
        always
        {
            sh 'ansible-playbook --tags cleanup -i inventory.yaml build.yaml'
        }
    }
}