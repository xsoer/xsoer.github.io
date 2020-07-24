fn read_dir(path: &Path) -> io::Result<()> {
    let mut entries = fs::read_dir(path)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;

    // The order in which `read_dir` returns entries is not guaranteed. If reproducible
    // ordering is required the entries should be explicitly sorted.

    entries.sort();

    // The entries have now been sorted by their path.
    println!("{:#?}", entries);
    Ok(())
}

fn print_file(entry: &DirEntry) {
    println!(
        "files-->{:#?}, file_name--->{:#?}, file_type--->{:#?}",
        entry.path(),
        entry.file_name(),
        entry.file_type()
    );
}

// one possible implementation of walking a directory only visiting files
fn visit_dirs(dir: &Path, cb: &dyn Fn(&DirEntry)) -> io::Result<()> {
    if dir.is_dir() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            // println!("{:#?}", path);
            if path.is_dir() {
                visit_dirs(&path, cb)?;
            } else {
                cb(&entry);
            }
        }
    }
    Ok(())
}

fn iter_env() {
    for arg in env::args() {
        println!("{}", arg);
    }
}

fn iter_env_vars() {
    for (key, value) in env::vars() {
        println!("{}: {}", key, value);
    }
}

fn dirs() {
    let path = env::current_dir().unwrap();
    println!("{}", path.display());
}

use std::io;

type AvlTreeNode = Option<Box<FileTree>>;

#[derive(Debug, Clone)]
struct FileTree {
    name: String,
    children: Vec<AvlTreeNode>,
    files: Vec<String>,
}

fn walk_dir_tree(path: &Path) {
    let mut file_tree = FileTree {
        name: path.to_str().unwrap().to_string(),
        children: [].to_vec(),
        files: vec![],
    };
    let res = dir_tree(path, &mut file_tree);
    println!("{:#?}", res);
    println!("file tree {:#?}", file_tree)
}

fn dir_tree(p: &Path, file_tree: &mut FileTree) -> io::Result<()> {
    if p.is_dir() {
        file_tree.name = p.to_str().unwrap().to_string();
        for entry in fs::read_dir(p)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_dir() {
                let mut child = FileTree {
                    name: path.to_str().unwrap().to_string(),
                    children: [].to_vec(),
                    files: [].to_vec(),
                };
                // file_tree.children.push(Some(Box::new(child)));
                dir_tree(&path, &mut child);
            } else {
                let p = path.to_str().unwrap().to_string();
                file_tree.files.push(p);
            }
        }
    }
    Ok(())
}
