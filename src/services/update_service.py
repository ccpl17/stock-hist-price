def normalize(version):
    return [int(i) for i in version.split(".")]


def check_for_update(current_version, remote_version):
    current_version = normalize(current_version)
    remote_version = normalize(remote_version)

    for i in range(max(len(current_version), len(remote_version))):
        if i >= len(current_version):
            current_version.append(0)
        if i >= len(remote_version):
            remote_version.append(0)

        if current_version[i] < remote_version[i]:
            return True
        elif current_version[i] > remote_version[i]:
            return False


def update_available(current_version, remote_version):
    if check_for_update(current_version, remote_version):
        return True
    else:
        return False
