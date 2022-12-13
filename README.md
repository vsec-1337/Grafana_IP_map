# Grafana_IP_map

## Local database to add for Grafana connection IP mapping


### Grafana MAP request :

```
SELECT
UNIX_TIMESTAMP(`timestamp`) as time_sec,
  `latitude` as latitude,
  `longitude` as longitude,
  COUNT(`ip`) AS value,
  `ip` as name
FROM live_ips
WHERE $__timeFilter(`timestamp`)
GROUP BY `ip`, `timestamp`, `latitude`, `longitude`
ORDER BY `timestamp` ASC
```
