# short-key-list

`short-key-list` publishes a rotating list of `200` tested VLESS keys collected from public upstream sources.

Every update cycle the pipeline:

- aggregates keys from several public lists;
- removes duplicates;
- validates candidates through a real `xray` outbound;
- sends a live request to `https://www.gstatic.com/generate_204`;
- keeps per-key historical ratings across runs;
- publishes a final list of `200` working keys chosen from the successful set.

The current public output lives here:

- `data/short-key-list.txt`

## What makes this list different

This repository does not mirror raw upstream dumps.

It tries to keep the published list usable by checking keys at publish time and by giving more weight to keys that have a better success history. The result is still dynamic, but it is not random noise:

- dead or obviously broken entries are filtered out;
- duplicate keys are removed before validation;
- keys with stronger recent history are more likely to stay in the final `200`;
- unstable keys can still appear, but much less often than consistently healthy ones.

## Validation model

For each candidate key the checker:

1. parses the VLESS link;
2. optionally performs a cheap TCP precheck;
3. starts a temporary local `xray` config for that key;
4. sends a real HTTP request through the proxy;
5. records the result in a persistent rating file;
6. rebuilds the final public list from the keys that passed.

The goal is practical filtering, not a guarantee that a key will stay alive forever after publication.

## Upstream sources

Default sources:

- `https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt`
- `https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt`
- `https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt`

## Repository layout

- `data/short-key-list.txt` — published public list.
- `scripts/check_key_list.py` — validator and rating-aware selector.
- `scripts/run_pipeline.py` — end-to-end runner.
- `scripts/publish_key_list.py` — publish step for git updates.
- `deploy/systemd/` — example service and timer units.

## For operators

This repository is public, but operational secrets are not stored in git:

- `.env` stays only on the server;
- runtime ratings stay in `state/key-ratings.json` on the server;
- the published repository only receives the final list and code changes.

Minimal local run:

```bash
cp .env.example .env
python3 scripts/run_pipeline.py
```
