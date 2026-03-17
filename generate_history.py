#!/usr/bin/env python3
"""
Fake GitHub Contribution History Generator

Creates ~4,000 backdated commits (2013-2026) with satirical era-themed
commit messages and plausible file changes. Push the resulting repo to
GitHub to fill your contribution graph.

Usage:
    python3 generate_history.py
"""

import os
import random
import subprocess
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42
START_DATE = datetime(2013, 1, 1)
END_DATE = datetime(2026, 3, 17)
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Era definitions
# ---------------------------------------------------------------------------

ERAS = [
    ("jquery",        datetime(2013, 1, 1),  datetime(2014, 6, 30)),
    ("angular",       datetime(2014, 7, 1),  datetime(2015, 12, 31)),
    ("react",         datetime(2016, 1, 1),  datetime(2017, 6, 30)),
    ("microservices", datetime(2017, 7, 1),  datetime(2019, 6, 30)),
    ("covid",         datetime(2019, 7, 1),  datetime(2021, 6, 30)),
    ("ai_hype",       datetime(2021, 7, 1),  datetime(2023, 12, 31)),
    ("vibe",          datetime(2024, 1, 1),  datetime(2026, 3, 17)),
]

# ---------------------------------------------------------------------------
# Commit message templates — era-specific
# ---------------------------------------------------------------------------

JQUERY_MESSAGES = [
    "Fix IE{v} rendering bug that only appears on Tuesdays",
    "Add jQuery plugin for {thing}",
    "Replace hand-rolled AJAX with $.ajax like a civilized person",
    "Fix z-index war — current winner: {n}",
    "Remove console.log that was there since the Bush administration",
    "Add polyfill for {feature} because IE{v} exists",
    "Fix PHP notice that somehow crashes the homepage",
    "Move inline styles to stylesheet like an adult",
    "Fix dropdown that opens upward on IE{v}",
    "Update jQuery from 1.{n} to 1.{m} — pray nothing breaks",
    "Add !important to fix specificity battle we lost",
    "Fix Flash fallback for browsers that deserve it",
    "Replace document.write with literally anything else",
    "Fix layout that breaks at exactly 1024px",
    "Stack Overflow said to do it this way",
    "Remove Dreamweaver artifacts from HTML",
    "Fix table-based layout that somehow still works",
    "Add clearfix hack because floats are a lifestyle",
    "Replace alert() debugging with actual console.log",
    "Fix CORS issue by adding Access-Control-Allow-* to everything",
    "Add loading spinner gif because users need entertainment",
    "Fix PHP session that expires during lunch",
    "Replace onclick handlers with proper jQuery bindings",
    "Fix modal that opens behind the overlay",
    "Update Bootstrap from 2.x — everything is different now",
    "Fix form validation that only works with JavaScript enabled",
    "Add vendor prefixes for {feature} — all four of them",
    "Fix WordPress plugin conflict number {n}",
    "Remove Geocities-era marquee tag from footer",
    "Fix PNG transparency for IE6 holdouts",
    "Replace FTP deployment with something from this decade",
    "Fix SQL injection that has been there since 2009",
    "Add responsive meta tag — welcome to the mobile era",
    "Fix favicon that has been a broken image since launch",
    "Remove commented-out code older than some interns",
    "Fix date picker that thinks February has 30 days",
    "Add Google Analytics — management wants numbers",
    "Fix carousel that carousels into the void",
    "Replace homegrown templating with Mustache",
    "Fix 500 error that only happens on the production server",
]

ANGULAR_MESSAGES = [
    "Refactor controller — it was 800 lines of $scope soup",
    "Fix digest cycle that achieves perpetual motion",
    "Add Grunt task for {thing}",
    "Replace Bower dependency with npm — the future is now",
    "Fix $scope.$watch that watches your CPU melt",
    "Add Angular directive for {thing}",
    "Fix two-way binding that binds in three ways somehow",
    "Migrate from Grunt to Gulp because streams are the future",
    "Fix ng-repeat that renders the entire DOM twice",
    "Add unit tests — first ones ever in this project",
    "Fix Angular service that was actually a factory that was actually a provider",
    "Remove $rootScope event that broadcasts to the void",
    "Fix minification bug — inject dependencies properly",
    "Add LESS preprocessing because CSS is too readable",
    "Fix route that resolves after the heat death of the universe",
    "Replace $http with Restangular for reasons nobody remembers",
    "Fix ng-click that fires on ng-blur which triggers ng-change",
    "Add e2e tests with Protractor — may God help us",
    "Fix filter that filters itself into nonexistence",
    "Remove angular.copy from hot path — it was copying reality",
    "Fix animation that animates the wrong element impressively",
    "Add lodash for one function we could have written ourselves",
    "Fix TypeScript compilation — any any any any",
    "Replace callback pyramid with promises",
    "Fix ng-if vs ng-show confusion — visible but doesn't exist",
    "Add ESLint and immediately disable 40 rules",
    "Fix template cache that caches yesterday's bugs",
    "Remove ui-router state that leads to existential void",
    "Fix factory that produces existential dread",
    "Add Sass because nesting CSS feels powerful",
    "Fix controller-as syntax migration — this vs $scope deathmatch",
    "Replace hand-rolled modal with ui-bootstrap",
    "Fix interceptor that intercepts its own requests",
    "Add component architecture — Angular 2 is coming someday",
    "Fix watchers count — down from 847 to 846",
    "Remove jQuery — Angular said we don't need it (we do)",
    "Fix race condition between two $http calls arguing",
    "Add code splitting — bundle was 4MB",
    "Fix test that passes locally and fails on Jenkins with contempt",
    "Replace string concatenation with template literals cautiously",
]

REACT_MESSAGES = [
    "Rewrite {thing} as React component",
    "Fix webpack config — attempt number {n}",
    "Add Redux because prop drilling hit the Earth's core",
    "Fix component that re-renders on every cosmic ray",
    "Eject from create-react-app — no going back now",
    "Replace setState callback with componentDidUpdate regret",
    "Fix key prop warning — just use index (I know, I know)",
    "Add CSS modules because className conflicts are violence",
    "Fix Redux action that dispatches existential crisis",
    "Migrate from npm to yarn because lockfiles matter apparently",
    "Add React Router — broke all existing links naturally",
    "Fix shouldComponentUpdate — it shouldn't, but it does",
    "Replace Redux thunk with saga — trading complexity for complexity",
    "Add Flow types and immediately suppress 200 errors",
    "Fix webpack dev server that serves yesterday's bundle",
    "Add hot module replacement — now bugs update in real-time",
    "Fix lifecycle method called in wrong order by physics",
    "Replace class component with... another class component (not ready yet)",
    "Add Storybook for component nobody else will look at",
    "Fix npm audit warnings — only 847 vulnerabilities remain",
    "Add Prettier because we can't agree on semicolons",
    "Fix babel config — plugins ordered by zodiac compatibility",
    "Replace moment.js — it was 70% of the bundle",
    "Add PropTypes that we will ignore in production",
    "Fix render method that is basically a novella",
    "Add enzyme tests that test implementation details lovingly",
    "Fix HOC wrapper that wraps wrappers wrapping wrappers",
    "Replace string refs with callback refs with createRef with useRef",
    "Add error boundary — errors now have a nice place to land",
    "Fix context API usage — prop drilling was simpler honestly",
    "Add code splitting with React.lazy — suspenseful",
    "Fix CSS-in-JS performance — styled-components was too styled",
    "Replace Redux with MobX because observable pain is better",
    "Add server-side rendering — doubled the bugs for free",
    "Fix package.json — remove 40 unused dependencies optimistically",
    "Add TypeScript — 'any' count so far: {n}",
    "Fix webpack tree shaking — it shook out the wrong tree",
    "Replace componentWillMount with getDerivedStateFromProps carefully",
    "Add linting rules then immediately add eslint-disable comments",
    "Fix build that takes longer than the feature it builds",
]

MICROSERVICES_MESSAGES = [
    "Split monolith into microservice — regret count: {n}",
    "Add Docker container for {thing}",
    "Fix Kubernetes pod that keeps restarting out of spite",
    "Add service mesh because direct HTTP was too simple",
    "Fix race condition between {n} microservices",
    "Add Prometheus metrics for monitoring our monitoring",
    "Replace REST with gRPC for internal service that has 2 callers",
    "Fix Docker image — was 2.3GB, now 2.1GB (progress)",
    "Add circuit breaker for service that breaks circuits",
    "Fix Helm chart values that value nothing",
    "Add Kafka for event streaming between two services",
    "Fix service discovery that can't discover itself",
    "Replace ELK stack with different ELK stack",
    "Add Terraform for infrastructure we'll never destroy",
    "Fix container networking — packets enter but don't leave",
    "Add health check endpoint that lies about being healthy",
    "Fix Kubernetes RBAC — everyone is admin, nobody is happy",
    "Replace microservice with function that was always a function",
    "Add Istio sidecar — now every pod has a friend",
    "Fix deployment pipeline that deploys to wrong environment",
    "Add distributed tracing to trace our distributed problems",
    "Fix memory leak in container — OOMKilled with dignity",
    "Replace Redis cache with bigger Redis cache",
    "Add API gateway — one more thing to configure and forget",
    "Fix secret management — secrets were in the Dockerfile",
    "Add auto-scaling that scales our AWS bill",
    "Fix microservice that calls itself in a loop philosophically",
    "Replace AWS Lambda with container because cold starts are cold",
    "Add retry logic with exponential backoff and exponential hope",
    "Fix Kubernetes ingress — traffic flows like a maze",
    "Add GraphQL federation because REST was too straightforward",
    "Fix Docker compose that only works on the original author's laptop",
    "Replace Consul with etcd because distributed consensus is fun",
    "Add canary deployment — the canary did not survive",
    "Fix log aggregation — now we can search our confusion faster",
    "Add chaos engineering — found chaos, still engineering",
    "Fix CORS across 7 microservices — each with different opinions",
    "Replace message queue — RabbitMQ to SQS to Kafka to NATS to despair",
    "Add Kubernetes namespace for team that has one service",
    "Fix container that works in Docker but not in Kubernetes naturally",
]

COVID_MESSAGES = [
    "Fix bug while adjusting to WFH life",
    "Add dark mode because we live in darkness now",
    "Fix Zoom integration — mic was muted the whole time",
    "Replace office whiteboard with Miro board nobody updates",
    "Add async standup because timezones are a social construct",
    "Fix VPN connection that drops during every demo",
    "Add Slack notification for {thing}",
    "Fix home office setup — cat walked on keyboard during deploy",
    "Replace in-person review with PR comments (less confrontational)",
    "Add accessibility features — should have done this years ago",
    "Fix production bug while kids attend school on same WiFi",
    "Add WebSocket support for real-time collaboration nobody asked for",
    "Fix Docker desktop eating all RAM alongside Chrome and Slack",
    "Replace daily standup with daily Slack novel",
    "Add end-to-end encryption because compliance said so",
    "Fix timezone bug — meeting was at 3am for someone",
    "Add remote pair programming support — screen share hell",
    "Fix notification fatigue — 47 channels and counting",
    "Replace Jira workflow with simpler Jira workflow (still complex)",
    "Add health check dashboard — both the app and personal kind",
    "Fix WiFi-dependent test that passes only near the router",
    "Add GitHub Actions to replace Jenkins VM nobody can access from home",
    "Fix blur background in video call — bookshelf was embarrassing",
    "Replace synchronous workflow with async everything",
    "Add offline mode because internet is a shared family resource",
    "Fix SSO that locks everyone out every Monday at 9am",
    "Add Tailwind CSS because writing CSS classes is too 2019",
    "Fix performance regression — works fine on office hardware though",
    "Replace watercooler chat with #random channel existentialism",
    "Add feature flag for feature nobody is sure about",
    "Fix memory leak discovered only because laptop fans are jet engines",
    "Add metrics dashboard to prove we're working from home",
    "Fix deployment that only works from office IP range",
    "Replace team lunch with team Zoom — cameras optional, pants optional",
    "Add sourdough starter tracking module (just kidding) (mostly)",
    "Fix daylight saving time bug — twice a year, every year",
    "Add progressive web app support — native apps are over (again)",
    "Fix caching bug that served yesterday's data like cold pizza",
    "Replace monorepo debate with bikeshedding on a different topic",
    "Add rate limiting after bot discovered our unprotected API",
]

AI_HYPE_MESSAGES = [
    "Add AI-powered {thing} (it's an if-else statement)",
    "Fix ML model that predicts the past with 99% accuracy",
    "Replace business logic with ChatGPT API call (what could go wrong)",
    "Add blockchain integration — manager saw a TED talk",
    "Fix NFT metadata endpoint — still not sure what we're doing",
    "Add Web3 login that takes 45 seconds and costs $12",
    "Replace recommendation engine with 'people also bought: random'",
    "Fix AI chatbot that tells customers to contact the AI chatbot",
    "Add GPT-generated release notes — they're technically accurate",
    "Fix crypto wallet integration nobody uses including us",
    "Add machine learning pipeline for problem solvable by SQL query",
    "Replace pivot to crypto with pivot back from crypto",
    "Fix hallucinating AI that confidently returns wrong answers",
    "Add vector database for embeddings of our embeddings",
    "Fix Web3 smart contract — it was neither smart nor contractual",
    "Replace manual process with AI that requires manual review",
    "Add LLM-powered search that searches for meaning in life",
    "Fix tokenizer that tokenizes our budget into nothing",
    "Add AI ethics review — the AI reviewed itself and passed",
    "Replace human judgment with model.predict() — HR is concerned",
    "Fix prompt injection vulnerability — users are creative",
    "Add stable diffusion for placeholder images nobody asked for",
    "Fix transformer model that transforms expectations into disappointment",
    "Replace data pipeline with Spark job that processes 3 rows",
    "Add AI feature because competitors added AI feature",
    "Fix model drift — it drifted into production somehow",
    "Add RAG pipeline that retrieves and generates confusion",
    "Replace cron job with 'AI agent' that runs on a cron job",
    "Fix embedding dimensions — 1536 dimensions of sadness",
    "Add LangChain integration with {n} unnecessary abstractions",
    "Fix AI code review that approved its own bugs",
    "Replace intern with GPT — intern was more reliable honestly",
    "Add neural network for problem that needed a hashmap",
    "Fix GPU memory leak — $400/day in cloud compute says hello",
    "Add responsible AI disclaimer to irresponsible AI feature",
    "Fix fine-tuned model that forgot how to do the original task",
    "Replace knowledge base with RAG — now nobody finds anything",
    "Add AI-powered dashboard — it dashboards with intelligence",
    "Fix token limit by summarizing the summary of the summary",
    "Add DAO governance module that governs nothing democratically",
]

VIBE_MESSAGES = [
    "Vibe-coded this entire feature — tests pending (forever)",
    "Fix bug Copilot introduced and Copilot cannot fix",
    "Add Claude-generated boilerplate — it's actually pretty good",
    "Replace manual coding with prompt engineering and prayer",
    "Fix AI-generated code that AI-generated tests say is fine",
    "Add cursor rules so the AI writes code the way I pretend to",
    "Vibe check: this function passes vibes but not tests",
    "Fix hallucinated API endpoint that sounded really convincing",
    "Add .cursorrules because apparently I manage AI coworkers now",
    "Replace code review with 'the AI wrote it so it must be right'",
    "Fix TypeScript types that Copilot made up confidently",
    "Add AI pair programming — it programs, I watch and approve",
    "Vibe-coded the vibe-coded code's vibe-coded tests",
    "Fix dependency suggested by AI that doesn't exist on npm",
    "Add LLM fallback for when the primary LLM is feeling creative",
    "Replace 'works on my machine' with 'works in my prompt'",
    "Fix function that Claude wrote — Claude also wrote this fix",
    "Add feature via natural language — future is weird",
    "Vibe refactor: same code, better energy",
    "Fix AI-generated regex that matches everything including regret",
    "Add Copilot-suggested optimization that optimizes nothing faster",
    "Replace architecture meeting with 'ask Claude about it'",
    "Fix prompt that generates the prompt that generates the code",
    "Add agentic workflow that agents its way into production",
    "Vibe-coded at 2am — the vibes were questionable",
    "Fix context window overflow — too much vibe, not enough window",
    "Add AI guardrails for AI that adds AI guardrails",
    "Replace documentation with 'ask the AI, it knows'",
    "Fix model that was deprecated between starting and finishing this PR",
    "Add Claude Code to fix what Claude Code generated",
    "Vibe-coded a config file — even YAML has vibes now",
    "Fix token budget — this conversation cost $4.50",
    "Add MCP server for {thing} because why not",
    "Replace manual deploy with AI agent that deploys and apologizes",
    "Fix agentic loop that achieved consciousness and resigned",
    "Add structured output to unstructured codebase — irony noted",
    "Vibe-coded the migration — the data vibed to a new table",
    "Fix AI review comment that was passive-aggressive and correct",
    "Add eval framework to evaluate if evaluations evaluate correctly",
    "Replace standup with AI summary — more accurate, less human",
]

UNIVERSAL_MESSAGES = [
    "Fix typo in fix for previous typo",
    "Merge branch 'hotfix' into 'regret'",
    "Remove code that was 'temporary' for {n} years",
    "Add TODO that will outlive this repository",
    "Fix bug introduced in previous bug fix",
    "Update dependencies — break nothing (impossible)",
    "Revert revert of revert — we're back to square one",
    "Add logging that will never be read",
    "Fix race condition that only races on Fridays",
    "Remove dead code that was already dead code's dead code",
    "Add config option nobody will ever change",
    "Fix test that tests nothing but its own existence",
    "Merge branch 'feature' into 'chaos'",
    "Update README that nobody reads",
    "Fix edge case that shouldn't be possible but here we are",
    "Add error handling for error that has never occurred",
    "Remove print statements added during last panic",
    "Fix lint warnings — the linter has spoken",
    "Add retry logic — if at first you don't succeed",
    "Fix date formatting — timezones were a mistake",
    "Refactor function that has been refactored {n} times",
    "Add monitoring for the thing that already broke",
    "Fix null check — null found a way",
    "Remove feature flag from 2 years ago — feature won",
    "Update .gitignore — too little too late",
    "Fix memory leak that leaks memories",
    "Add caching that expires before being useful",
    "Fix pagination that skips page {n}",
    "Merge branch 'experiment' into 'consequences'",
    "Remove commented-out code and its commented-out comments",
    "Fix build that builds character more than software",
    "Add index to database query that takes a coffee break",
    "Fix CSS that works in Chrome and nowhere else",
    "Update changelog — technically this counts as a change",
    "Fix flaky test by making it flakier then fixing that",
    "Add validation that validates the validator",
    "Remove unused import that was providing moral support",
    "Fix encoding issue — UTF-8 is a suggestion apparently",
    "Merge branch 'main' into 'main' somehow",
    "Add fallback for fallback's fallback",
]

ERA_MESSAGES = {
    "jquery": JQUERY_MESSAGES,
    "angular": ANGULAR_MESSAGES,
    "react": REACT_MESSAGES,
    "microservices": MICROSERVICES_MESSAGES,
    "covid": COVID_MESSAGES,
    "ai_hype": AI_HYPE_MESSAGES,
    "vibe": VIBE_MESSAGES,
}

# Fill-in values for parameterized templates
THINGS = [
    "tooltip", "dropdown", "modal", "sidebar", "navbar", "carousel",
    "accordion", "datepicker", "autocomplete", "tabs", "breadcrumbs",
    "pagination", "toast notification", "progress bar", "search bar",
    "file uploader", "color picker", "slider", "login form", "dashboard",
    "settings page", "user profile", "notification bell", "checkout flow",
    "onboarding wizard", "analytics tracker", "feature toggle", "API client",
    "auth middleware", "rate limiter", "cache layer", "logging service",
    "error reporter", "health monitor", "config loader", "theme switcher",
]

FEATURES = [
    "border-radius", "flexbox", "grid", "placeholder", "opacity",
    "transform", "transition", "animation", "box-shadow", "gradient",
    "media queries", "viewport units", "calc()", "custom properties",
]

IE_VERSIONS = [6, 7, 8, 9, 10, 11]


def fill_template(template, rng):
    """Replace {placeholders} with random values."""
    result = template
    if "{thing}" in result:
        result = result.replace("{thing}", rng.choice(THINGS), 1)
    if "{feature}" in result:
        result = result.replace("{feature}", rng.choice(FEATURES), 1)
    if "{v}" in result:
        result = result.replace("{v}", str(rng.choice(IE_VERSIONS)), 1)
    if "{n}" in result:
        result = result.replace("{n}", str(rng.randint(2, 47)), 1)
    if "{m}" in result:
        result = result.replace("{m}", str(rng.randint(8, 12)), 1)
    return result


def get_era(date):
    """Return the era name for a given date."""
    for name, start, end in ERAS:
        if start <= date <= end:
            return name
    return "vibe"


def pick_message(date, rng):
    """Pick a commit message: 60% era-specific, 40% universal."""
    era = get_era(date)
    if rng.random() < 0.6:
        templates = ERA_MESSAGES[era]
    else:
        templates = UNIVERSAL_MESSAGES
    return fill_template(rng.choice(templates), rng)


# ---------------------------------------------------------------------------
# Frequency model
# ---------------------------------------------------------------------------

def get_career_multiplier(date):
    """Activity ramps up over career: 0.7 (2013) -> 1.0 (2018) -> 1.1 (2024+)."""
    year = date.year + date.month / 12.0
    if year < 2018:
        return 0.7 + 0.3 * (year - 2013) / 5.0
    return min(1.1, 1.0 + 0.1 * (year - 2018) / 6.0)


def get_month_multiplier(date):
    """January boost (1.3x), December cooldown (0.5x)."""
    if date.month == 1:
        return 1.3
    if date.month == 12:
        return 0.5
    return 1.0


def generate_yearly_events(year, rng):
    """Generate vacation gaps, sprint bursts, and burnout dips for a year."""
    events = []

    # 2-3 vacation weeks
    for _ in range(rng.randint(2, 3)):
        start_day = rng.randint(1, 340)
        start = datetime(year, 1, 1) + timedelta(days=start_day)
        events.append(("vacation", start, start + timedelta(days=rng.randint(5, 9))))

    # 4-6 sprint bursts (1-2 weeks each)
    for _ in range(rng.randint(4, 6)):
        start_day = rng.randint(1, 340)
        start = datetime(year, 1, 1) + timedelta(days=start_day)
        events.append(("sprint", start, start + timedelta(days=rng.randint(5, 14))))

    # 1-2 burnout dips
    for _ in range(rng.randint(1, 2)):
        start_day = rng.randint(1, 320)
        start = datetime(year, 1, 1) + timedelta(days=start_day)
        events.append(("burnout", start, start + timedelta(days=rng.randint(14, 28))))

    return events


def get_event_multiplier(date, yearly_events):
    """Check if date falls in a special period."""
    year = date.year
    if year not in yearly_events:
        return 1.0
    for event_type, start, end in yearly_events[year]:
        if start <= date <= end:
            if event_type == "vacation":
                return 0.0
            if event_type == "sprint":
                return 1.8
            if event_type == "burnout":
                return 0.3
    return 1.0


def get_base_probability(date):
    """Base commit probability by day of week."""
    dow = date.weekday()  # 0=Mon, 6=Sun
    if dow < 5:
        return 0.55
    if dow == 5:
        return 0.20
    return 0.12


def pick_commit_count(rng):
    """When active, how many commits."""
    r = rng.random()
    if r < 0.50:
        return 1
    if r < 0.80:
        return 2
    if r < 0.92:
        return 3
    if r < 0.97:
        return 4
    return rng.randint(5, 7)


def get_commit_count(date, yearly_events, rng):
    """Determine number of commits for a given date."""
    base = get_base_probability(date)
    multiplier = (
        get_career_multiplier(date)
        * get_month_multiplier(date)
        * get_event_multiplier(date, yearly_events)
    )
    probability = min(base * multiplier, 0.95)

    if probability <= 0:
        return 0
    if rng.random() > probability:
        return 0
    return pick_commit_count(rng)


# ---------------------------------------------------------------------------
# Time-of-day distribution
# ---------------------------------------------------------------------------

def pick_time(date, rng):
    """Pick a random time of day for the commit."""
    dow = date.weekday()
    r = rng.random()

    if dow < 5:  # Weekday
        if r < 0.70:
            hour = rng.randint(9, 17)
        elif r < 0.95:
            hour = rng.randint(18, 22)
        else:
            hour = rng.randint(0, 2)
    else:  # Weekend
        if r < 0.60:
            hour = rng.randint(10, 15)
        else:
            hour = rng.randint(16, 21)

    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    return date.replace(hour=hour, minute=minute, second=second)


# ---------------------------------------------------------------------------
# File changes — plausible diffs
# ---------------------------------------------------------------------------

# Files available by era (introduced gradually)
ERA_FILE_INTROS = {
    2013: ["README.md", "src/app.js"],
    2014: ["src/utils.js", "src/config.js"],
    2015: [".gitignore", "package.json"],
    2016: ["src/components.js", "tests/test_app.js"],
    2017: ["docs/guide.md", "src/api.js"],
    2018: ["src/middleware.js", "docker-compose.yml"],
    2019: ["src/services.js", ".env.example"],
    2020: ["src/hooks.js", "tests/test_utils.js"],
    2021: ["src/types.js", "scripts/deploy.sh"],
    2022: ["src/ai.js", "src/analytics.js"],
    2023: ["src/agents.js", "src/embeddings.js"],
    2024: [".cursorrules", "src/prompts.js"],
    2025: ["src/mcp.js", "src/tools.js"],
    2026: ["src/vibes.js"],
}

CHANGELOG_ENTRIES = [
    "- Fixed {thing} alignment issue",
    "- Updated {thing} error handling",
    "- Improved {thing} performance",
    "- Added {thing} validation",
    "- Refactored {thing} logic",
    "- Resolved {thing} compatibility issue",
    "- Enhanced {thing} user experience",
    "- Patched {thing} security vulnerability",
]

SOURCE_COMMENTS = [
    "// TODO: Revisit this later",
    "// HACK: This works but I don't know why",
    "// FIXME: Edge case not handled",
    "// NOTE: Do not remove — breaks production",
    "// OPTIMIZE: This is O(n^2) but n is always small (famous last words)",
    "// DEPRECATED: Use the new version (which doesn't exist yet)",
    "// WORKAROUND: Library bug — see issue #{}",
    "// MAGIC NUMBER: 42 — the answer to everything",
    "// TEMPORARY: Added 3 years ago",
    "// REVIEW: Is this right? Asking for a friend",
]

CONFIG_VERSIONS = [
    '  "version": "{}.{}.{}"',
]


class FileManager:
    """Manages the simulated file system and generates plausible changes."""

    def __init__(self, repo_dir, rng):
        self.repo_dir = repo_dir
        self.rng = rng
        self.file_lines = {}  # path -> list of lines
        self.available_files = set()
        self.commit_number = 0

    def get_available_files(self, date):
        """Update available files based on date."""
        for year, files in ERA_FILE_INTROS.items():
            if date.year >= year:
                for f in files:
                    if f not in self.available_files:
                        self.available_files.add(f)
        return list(self.available_files)

    def ensure_dirs(self, filepath):
        """Create directories for a file path."""
        dirpath = os.path.join(self.repo_dir, os.path.dirname(filepath))
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)

    def read_or_init(self, filepath):
        """Read file contents or initialize empty."""
        if filepath not in self.file_lines:
            full = os.path.join(self.repo_dir, filepath)
            if os.path.exists(full):
                with open(full, "r") as f:
                    self.file_lines[filepath] = f.readlines()
            else:
                self.file_lines[filepath] = []
        return self.file_lines[filepath]

    def write_file(self, filepath, lines):
        """Write lines to file."""
        self.file_lines[filepath] = lines
        self.ensure_dirs(filepath)
        full = os.path.join(self.repo_dir, filepath)
        with open(full, "w") as f:
            f.writelines(lines)

    def trim_if_long(self, filepath, max_lines=500):
        """Trim file if too long (simulate refactoring)."""
        lines = self.read_or_init(filepath)
        if len(lines) > max_lines:
            # Keep first 50 and last 50 lines
            self.write_file(filepath, lines[:50] + ["\n", "// ... refactored ...\n", "\n"] + lines[-50:])

    def make_change(self, date):
        """Make a plausible file change and return list of modified files."""
        available = self.get_available_files(date)
        if not available:
            return []

        self.commit_number += 1
        r = self.rng.random()

        if r < 0.30:
            return self._append_changelog(date)
        elif r < 0.50:
            return self._modify_config()
        elif r < 0.75:
            return self._add_source_comment(available)
        elif r < 0.85:
            return self._update_readme(date)
        elif r < 0.90:
            return self._add_small_file(date)
        elif r < 0.95:
            return self._update_gitignore()
        else:
            return self._update_deps()

    def _append_changelog(self, date):
        """Append entry to CHANGELOG.md."""
        lines = self.read_or_init("CHANGELOG.md")
        if not lines:
            lines = [f"# Changelog\n", "\n"]
        entry = fill_template(self.rng.choice(CHANGELOG_ENTRIES), self.rng)
        lines.append(f"\n## {date.strftime('%Y-%m-%d')}\n{entry}\n")
        self.write_file("CHANGELOG.md", lines)
        self.trim_if_long("CHANGELOG.md")
        return ["CHANGELOG.md"]

    def _modify_config(self):
        """Bump version in package.json or similar."""
        filepath = "package.json"
        lines = self.read_or_init(filepath)
        if not lines:
            lines = [
                '{\n',
                '  "name": "project",\n',
                '  "version": "0.1.0",\n',
                '  "description": "A project",\n',
                '  "main": "src/app.js",\n',
                '  "scripts": {\n',
                '    "start": "node src/app.js",\n',
                '    "test": "echo ok"\n',
                '  }\n',
                '}\n',
            ]
        # Update version line
        major = self.rng.randint(0, 3)
        minor = self.rng.randint(0, 30)
        patch = self.commit_number % 100
        for i, line in enumerate(lines):
            if '"version"' in line:
                lines[i] = f'  "version": "{major}.{minor}.{patch}",\n'
                break
        self.write_file(filepath, lines)
        return [filepath]

    def _add_source_comment(self, available):
        """Add a comment to a source file."""
        source_files = [f for f in available if f.endswith(".js")]
        if not source_files:
            source_files = ["src/app.js"]
        filepath = self.rng.choice(source_files)
        lines = self.read_or_init(filepath)
        if not lines:
            lines = [f"// {filepath}\n", "\n", "function init() {{\n", "  // initialized\n", "}}\n"]
        comment = self.rng.choice(SOURCE_COMMENTS)
        if "{}" in comment:
            comment = comment.replace("{}", str(self.rng.randint(100, 9999)))
        insert_pos = self.rng.randint(0, max(0, len(lines) - 1))
        lines.insert(insert_pos, comment + "\n")
        self.write_file(filepath, lines)
        self.trim_if_long(filepath)
        return [filepath]

    def _update_readme(self, date):
        """Write a short, static README.md — only the 'Last updated' line changes."""
        date_str = date.strftime("%Y-%m-%d")
        lines = [
            "# History\n",
            "\n",
            "A collection of utilities, experiments, and lessons learned over the years.\n",
            "\n",
            "## Setup\n",
            "\n",
            "```bash\n",
            "npm install\n",
            "npm start\n",
            "```\n",
            "\n",
            "## Usage\n",
            "\n",
            "See `src/` for source code and `docs/` for guides.\n",
            "\n",
            f"Last updated: {date_str}\n",
        ]
        self.write_file("README.md", lines)
        return ["README.md"]

    def _add_small_file(self, date):
        """Add a small new utility file."""
        names = [
            "src/helpers.js", "src/constants.js", "src/validators.js",
            "src/formatters.js", "src/parsers.js", "src/transforms.js",
            "scripts/setup.sh", "scripts/clean.sh", "docs/notes.md",
            "docs/api.md", "tests/test_helpers.js", "tests/fixtures.js",
        ]
        filepath = self.rng.choice(names)
        lines = self.read_or_init(filepath)
        if not lines:
            if filepath.endswith(".js"):
                lines = [
                    f"// {filepath}\n",
                    f"// Created {date.strftime('%Y-%m-%d')}\n",
                    "\n",
                    "module.exports = {};\n",
                ]
            elif filepath.endswith(".sh"):
                lines = [
                    "#!/bin/bash\n",
                    f"# {filepath}\n",
                    "echo 'Running...'\n",
                ]
            else:
                lines = [
                    f"# {os.path.basename(filepath).replace('.md', '').title()}\n",
                    "\n",
                    f"Last updated: {date.strftime('%Y-%m-%d')}\n",
                ]
        else:
            lines.append(f"// Updated {date.strftime('%Y-%m-%d')}\n")
        self.write_file(filepath, lines)
        return [filepath]

    def _update_gitignore(self):
        """Add entry to .gitignore."""
        lines = self.read_or_init(".gitignore")
        if not lines:
            lines = ["node_modules/\n", ".env\n", "dist/\n", ".DS_Store\n"]
        entries = [
            "*.log\n", "coverage/\n", ".cache/\n", "build/\n",
            "tmp/\n", "*.swp\n", ".idea/\n", ".vscode/\n",
            "__pycache__/\n", "*.pyc\n",
        ]
        new_entry = self.rng.choice(entries)
        if new_entry not in lines:
            lines.append(new_entry)
        self.write_file(".gitignore", lines)
        return [".gitignore"]

    def _update_deps(self):
        """Add a dependency to package.json."""
        filepath = "package.json"
        lines = self.read_or_init(filepath)
        if not lines:
            return self._modify_config()
        # Just bump the version as a proxy for dep changes
        return self._modify_config()


# ---------------------------------------------------------------------------
# Git operations
# ---------------------------------------------------------------------------

def run_git(args, env=None):
    """Run a git command in the repo directory."""
    cmd = ["git"] + args
    result = subprocess.run(
        cmd, cwd=REPO_DIR, capture_output=True, text=True, env=env
    )
    if result.returncode != 0 and "nothing to commit" not in result.stderr:
        # Silently ignore most errors to keep going
        pass
    return result


def init_repo():
    """Initialize git repo if needed."""
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        run_git(["init", "-b", "master"])
        # Configure local git user
        run_git(["config", "user.email", "admin@nathanbase.com"])
        run_git(["config", "user.name", "Nathan"])


def make_commit(message, date_str, files):
    """Stage files and create a backdated commit."""
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    for f in files:
        run_git(["add", f])

    run_git(["commit", "-m", message, "--allow-empty"], env=env)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    rng = random.Random(SEED)

    print("Initializing repository...")
    init_repo()

    # Pre-generate yearly events
    yearly_events = {}
    for year in range(2013, 2027):
        yearly_events[year] = generate_yearly_events(year, rng)

    file_mgr = FileManager(REPO_DIR, rng)
    total_commits = 0
    current = START_DATE

    print(f"Generating commits from {START_DATE.date()} to {END_DATE.date()}...")

    while current <= END_DATE:
        count = get_commit_count(current, yearly_events, rng)

        # Generate commits for this day, sorted by time
        times = sorted([pick_time(current, rng) for _ in range(count)])

        for commit_time in times:
            message = pick_message(current, rng)
            changed_files = file_mgr.make_change(current)

            if changed_files:
                date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
                make_commit(message, date_str, changed_files)
                total_commits += 1

                if total_commits % 200 == 0:
                    print(f"  {total_commits} commits generated... (currently at {current.date()})")

        current += timedelta(days=1)

    print(f"\nDone! Generated {total_commits} commits.")
    print(f"\nVerify with:")
    print(f"  git log --oneline | head -20")
    print(f"  git log --oneline | wc -l")
    print(f"\nTo push:")
    print(f"  git remote add origin git@github.com:<username>/<repo>.git")
    print(f"  git push -u origin master")


if __name__ == "__main__":
    main()
