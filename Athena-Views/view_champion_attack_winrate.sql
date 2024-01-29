CREATE OR REPLACE VIEW "view_champion_attack_winrate" AS 
SELECT
  mc.name champion
, cc.attack_damage attack_damage
, csr.win_rate win_rate
FROM
  ((main_champions mc
INNER JOIN champions_core_statistics cc ON (mc.champion_id = cc.champion_id))
INNER JOIN champions_irl_statistics csr ON (mc.name = csr.name))
