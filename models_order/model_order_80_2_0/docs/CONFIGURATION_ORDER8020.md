# Configuration ORDER80.2.0

Default configuration: `data/observation_config_8_0_2_0.json`.

## Duration

```json
{"duration":"24h"}
```

Accepted: seconds as a number or string, `s`, `m`, `h`, `d`, `week`, compound forms, and `forever`.

## RAG polling

```json
{
  "rag_inbox":"run_rag_inbox",
  "rag_poll_interval_seconds":15,
  "checkpoint_interval_seconds":60
}
```

Drop documentary files into `documents/` and formal JSON theorem certificates into `formal/`.

## Web

```json
{
  "web": {
    "enabled": true,
    "search_enabled": true,
    "search_variants_per_round": 3,
    "max_pages_per_round": 3,
    "link_depth": 1,
    "allow_domains": []
  }
}
```

`allow_domains` may be used to restrict retrieval. An empty list means no host restriction.

## Formal search limits

The ORDER80.2 defaults remain:

```json
{
  "max_observation_rounds_per_node": 0,
  "max_node_depth": 0,
  "max_node_attempts": 0,
  "max_search_states": 0,
  "max_depth": 32
}
```

`0` means no artificial limit for that parameter. The wall-clock `duration` is the main long-run budget.
