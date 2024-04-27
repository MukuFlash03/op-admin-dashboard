import re
import argparse

def generateUpdatedSuffix(current_image_name):
    try:
        pattern = "^(FROM\s+)(.+)(/)(.+)(:)(.+)(_)(\d{4}-\d{2}-\d{2}--\d{2}-\d{2})"
        matches = re.search(pattern, current_image_name)

        current_timestamp = matches.group(8)
        print("Current timestamp = %s" % current_timestamp)

        latest_timestamp = args.tag
        print("Latest timestamp = %s" % latest_timestamp)

        latest_image_name = ''.join([match for match in matches.groups()[:-1]]) + latest_timestamp + "\n"
        print("Current image name = %s" % current_image_name)
        print("Latest image name = %s" % latest_image_name)
        return latest_image_name
    except:
        print("No matching pattern found in FROM layer while parsing Dockerfile to replace tags.")
        return False

def updateDockerfile():
    docker_file_path = rf"{args.file}"
    docker_file = open(docker_file_path,"r")
    current_file_content = docker_file.readlines()
    docker_file.close()
    updated_file_content = []

    for line in current_file_content:
        if line.strip().startswith("FROM ") and not line.strip().startswith("#"):
            updatedTag = generateUpdatedSuffix(line)
            if updatedTag is False:
                updated_file_content.append(line)
            else:
                updated_file_content.append(updatedTag)
        else:
            updated_file_content.append(line)

    with open(docker_file_path,"w") as docker_file:
        docker_file.writelines(updated_file_content)

    docker_file = open(docker_file_path,"r")
    current_file_content = docker_file.readlines()
    docker_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Dockerfile path", required=True)
    parser.add_argument("-t", "--tag", help="Latest docker image tag", required=True)
    args = parser.parse_args()
    print(args)
    updateDockerfile()