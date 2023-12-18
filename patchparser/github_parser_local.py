        self.original_file_name = None
        self.current_file_name = None



        original_file_name = row["b_file"]
        current_file_name = row["a_file"]

            headers_search = re.findall(r"@@(.*?)@@", raw_file_patch)

                    original_header_lines = re.search(
                        f"@@ -(.*?) \+", f"@@{head_row}@@").group(1)

                        original_lines = re.search(
                            f"@@ -(.*?) \+", header).group(1)
                            original_line_start = int(
                                original_lines.split(",")[0])
                            original_line_length = int(
                                original_lines.split(",")[1])

                        modified_lines = re.search(
                            f" \+(.*) @@", header).group(1)
                            modified_line_start = int(
                                modified_lines.split(",")[0])
                            modified_line_length = int(
                                modified_lines.split(",")[1])


                    raw_patch = raw_file_patch[raw_file_patch.find(
                        headers[index])+len(headers[index]):]
                    raw_patch = raw_file_patch[raw_file_patch.find(
                        headers[index])+len(headers[index]):raw_file_patch.find(headers[index+1])]

                """Create a temporary class to hold the parsed patch data"""

                temp_parsed_commit.original_file_name = original_file_name
                temp_parsed_commit.current_file_name = current_file_name


            temp_parsed_commit.original_file_name = original_file_name
            temp_parsed_commit.current_file_name = current_file_name









        original_code=original_code_str,
        modified_code=modified_code_str,
        additions=additions,
        added_code=added_code_str,
        deletions=deletions,
        deleted_code=deleted_code_str,
        changes=changes









    #     # This doesn't appear in the Git repo?



        try:
                a_file = re.findall('(?= a\/)(.*?)(?=\\n)',
                                    file_diff)[0].split(' ')[1].strip()
                a_file = re.findall('(?= a\/)(.*?)(?=\\n)',
                                    file_diff)[1].strip()
                b_file = re.findall('(?= b\/)(.*?)(?=\\n)',
                                    file_diff)[0].strip()
                b_file = re.findall('(?= b\/)(.*?)(?=\\n)',
                                    file_diff)[1].strip()


                "filename": filename,
                "a_file": a_file,
                "b_file": b_file,
                "additions": commit_info.stats.files[filename]['insertions'],
                "deletions": commit_info.stats.files[filename]['deletions'],
                "changes": commit_info.stats.files[filename]['lines'],
                "patch": diff_file,
                "status": status



    return parsed_files


def commit_local_updated(repo_owner: str, repo_name: str, sha: str, base_repo_path: str, verbose=False) -> list:
    """Pass the local cloned GitHub repo_owner, repo_name, and associated commit to parse.

    Args:
        repo_owner (str): Target repo owner
        repo_name (str): Target repo name
        sha (str): Target commit SHA from GitHub
        base_repo_path (str): Directory of localy cloned repository

    Returns:
        list: List of dictionaries strcutred around the class CommitParseLocal
    """

    """Create the repo_path"""
    # repo_path = f"{base_repo_path}{repo_owner}/{repo_name}"
    repo_path = f"{base_repo_path}"

    """Commit info API URL"""
    repo = git.Repo(repo_path)

    # obtains the raw diff for a given SHA
    # SHA~ represents the prior commit
    diff = repo.git.diff(f"{sha}~", f"{sha}")

    # obtain commit information
    commit_info = repo.commit(sha)

    # obtain a commit diff
    git_repo_diff = commit_info.diff(f"{sha}~", create_patch=True)
    git_repo_diff_change_type = commit_info.diff(f"{sha}~")

    # split the raw diff, no need to take 0, it's empty on this split
    diff_splits = diff.split("diff --git")[1:]

    """Initialize a CommitParse to hold data"""
    parsed_commit = CommitParseLocal(repo_owner=repo_owner,
                                     repo_name=repo_name,
                                     sha=sha)

    """Add commit message"""
    parsed_commit.message = commit_info.message
    parsed_commit.commit_author_name = commit_info.author.name
    parsed_commit.commit_author_email = commit_info.author.email
    parsed_commit.commit_author_date = commit_info.authored_datetime
    parsed_commit.commit_committer_name = commit_info.committer.name
    parsed_commit.commit_committer_email = commit_info.committer.email
    parsed_commit.commit_committer_date = commit_info.committed_datetime
    parsed_commit.commit_tree_sha = commit_info.tree.hexsha
    parsed_commit.parents = [z.hexsha for z in commit_info.parents]

    """Create files list of dictionaries"""
    # creates a placeholder for the parsed raw diff
    files = []

    # create a commit info list
    commit_info_list = list(commit_info.stats.files)

    for index, file_diff in enumerate(git_repo_diff[:1000]):
        try:
            temp_parse_test = {
                "filename": file_diff.a_path,
                "a_file": file_diff.a_path,
                "b_file": file_diff.b_path,
                "additions": commit_info.stats.files[file_diff.a_path]['insertions'],
                "deletions": commit_info.stats.files[file_diff.a_path]['deletions'],
                "changes": commit_info.stats.files[file_diff.a_path]['lines'],
                "patch": file_diff.diff.decode("utf-8"),
                "status": git_repo_diff_change_type[index].change_type
            }

            files.append(temp_parse_test)
        except:
            print("wait")

    """Parse the files"""
    parsed_files = parse_commit_info(files, parsed_commit)
