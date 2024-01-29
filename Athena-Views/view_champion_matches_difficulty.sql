CREATE OR REPLACE VIEW "view_champion_matches_difficulty" AS 
SELECT
  mc.name champion
, csr.matches matches
, mc.difficulty difficulty
FROM
  (main_champions mc
INNER JOIN champions_irl_statistics csr ON (mc.name = csr.name))
