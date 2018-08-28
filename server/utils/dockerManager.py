import docker

class DockerManager:
    #Set connection to Docker from Socket
    client = docker.from_env()

    @classmethod
    def runContainer(cls,Name, command, hasOut, hasErr, Deatach):
        #Set connection to Docker from Socket
        client = docker.from_env()
        client.containers.run(Name, command, hasOut, hasErr, deatach=Deatach )

    @classmethod
    def printContainerList(cls):
        client = docker.from_env()
        return client.containers.list(all=True)
        