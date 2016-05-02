CREATE TABLE dictionary (
    id serial NOT NULL PRIMARY KEY,
    vocab text,
    baseform text,
    phongl text,
    grclassgl text,
    stylgl text,
    def text,
    anti text,
    leglexam text
);

CREATE MATERIALIZED VIEW v_dictionary AS
 SELECT dictionary.vocab,
    dictionary.def,
    dictionary.leglexam,
        CASE
            WHEN ((dictionary.leglexam <> ''::text) AND (dictionary.leglexam IS NOT NULL)) THEN ('. '::text || dictionary.leglexam)
            ELSE ''::text
        END AS def_w_exam
   FROM dictionary
  WHERE ((dictionary.def <> ALL (ARRAY[''::text, '+'::text])) AND (dictionary.def !~~ '==%'::text) AND (dictionary.def !~~ '<=%'::text) AND (dictionary.def !~~ '=>%'::text) AND (dictionary.vocab !~~ '%...'::text))
  WITH NO DATA;
