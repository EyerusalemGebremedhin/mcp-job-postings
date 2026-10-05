use serde::Deserialize;
use std::collections::HashMap;
use std::{env, fs, process};

#[derive(Deserialize)]
struct Posting {
    id: u32,
    title: String,
    company: String,
    location: String,
    skills: Vec<String>,
}

fn load(path: &str) -> Vec<Posting> {
    let text = fs::read_to_string(path).unwrap_or_else(|e| {
        eprintln!("Could not read {path}: {e}");
        process::exit(1);
    });
    serde_json::from_str(&text).unwrap_or_else(|e| {
        eprintln!("{path} is not valid postings JSON: {e}");
        process::exit(1);
    })
}

fn count_by_company(postings: &[Posting]) {
    let mut counts: HashMap<&str, u32> = HashMap::new();
    for p in postings {
        *counts.entry(p.company.as_str()).or_insert(0) += 1;
    }
    let mut rows: Vec<_> = counts.into_iter().collect();
    rows.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(b.0)));
    for (company, n) in rows {
        println!("{n:>3}  {company}");
    }
}

fn search_by_skill(postings: &[Posting], skill: &str) {
    let skill = skill.trim().to_lowercase();
    if skill.is_empty() {
        eprintln!("skill must not be empty. Example: rust");
        process::exit(1);
    }
    let hits: Vec<_> = postings
        .iter()
        .filter(|p| p.skills.iter().any(|s| s.to_lowercase() == skill))
        .collect();
    for p in &hits {
        println!("#{} {} at {} ({})", p.id, p.title, p.company, p.location);
    }
    println!("{} postings list '{}'", hits.len(), skill);
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let postings = load("data/postings.json");
    match args.first().map(String::as_str) {
        Some("count") => count_by_company(&postings),
        Some("skill") => match args.get(1) {
            Some(s) => search_by_skill(&postings, s),
            None => {
                eprintln!("Usage: skill <name>");
                process::exit(1);
            }
        },
        _ => {
            eprintln!("Usage: count | skill <name>");
            process::exit(1);
        }
    }
}