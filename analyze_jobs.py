#!/usr/bin/env python3
"""
Analyze and visualize job scraping results.
"""
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def load_jobs(file_path: str = "data/jobs_latest.json"):
    """Load jobs from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        print("Run the scraper first: poetry run jobminer")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in {file_path}")
        sys.exit(1)


def analyze_jobs(jobs):
    """Analyze job data and print statistics."""
    if not jobs:
        print("No jobs found!")
        return

    print("=" * 80)
    print("📊 JOB SCRAPING ANALYSIS")
    print("=" * 80)
    print()

    # Basic stats
    print(f"📈 Total Jobs: {len(jobs)}")
    print()

    # Jobs with scores
    scored_jobs = [j for j in jobs if j.get('relevance_score') is not None]
    if scored_jobs:
        avg_score = sum(j['relevance_score'] for j in scored_jobs) / len(scored_jobs)
        max_score = max(j['relevance_score'] for j in scored_jobs)
        min_score = min(j['relevance_score'] for j in scored_jobs)

        print(f"🎯 Relevance Scores:")
        print(f"   Average: {avg_score:.2f}")
        print(f"   Range: {min_score:.2f} - {max_score:.2f}")
        print()

    # Companies
    companies = Counter(j['company'] for j in jobs)
    print(f"🏢 Top 10 Companies by Job Count:")
    for company, count in companies.most_common(10):
        print(f"   {count:2d} - {company}")
    print()

    # Roles
    roles = Counter(j['title'] for j in jobs)
    print(f"💼 Top 10 Job Titles:")
    for role, count in roles.most_common(10):
        print(f"   {count:2d} - {role[:60]}")
    print()

    # Remote
    remote_count = sum(1 for j in jobs if j.get('is_remote'))
    print(f"🏠 Remote Jobs: {remote_count} ({remote_count/len(jobs)*100:.1f}%)")
    print()

    # Top scored jobs
    if scored_jobs:
        print("⭐ Top 15 Jobs by Relevance Score:")
        print()
        for i, job in enumerate(sorted(scored_jobs,
                                      key=lambda x: x.get('relevance_score', 0),
                                      reverse=True)[:15], 1):
            score = job.get('relevance_score', 0)
            company = job['company']
            title = job['title'][:50]

            # Score bar
            bar_length = int(score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)

            print(f"   {i:2d}. [{score:.2f}] {bar}")
            print(f"       {company} - {title}")
            print()

    print("=" * 80)


def export_filtered(jobs, min_score: float = 0.7, output_file: str = "data/top_jobs.json"):
    """Export jobs above a certain score threshold."""
    filtered = [j for j in jobs if j.get('relevance_score', 0) >= min_score]

    if not filtered:
        print(f"No jobs found with score >= {min_score}")
        return

    with open(output_file, 'w') as f:
        json.dump(filtered, f, indent=2)

    print(f"✅ Exported {len(filtered)} jobs (score >= {min_score}) to {output_file}")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze job scraping results")
    parser.add_argument('--file', '-f', default='data/jobs_latest.json',
                      help='Path to jobs JSON file')
    parser.add_argument('--export', '-e', action='store_true',
                      help='Export top jobs to separate file')
    parser.add_argument('--min-score', '-s', type=float, default=0.7,
                      help='Minimum score for export (default: 0.7)')

    args = parser.parse_args()

    jobs = load_jobs(args.file)
    analyze_jobs(jobs)

    if args.export:
        print()
        export_filtered(jobs, args.min_score)


if __name__ == '__main__':
    main()
