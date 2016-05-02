
-- create v_dictionary
create materialized view v_dictionary as
select vocab, def, leglexam
    , (
        case when leglexam != '' and leglexam is not null
            then '. ' || leglexam
            else '' end
    ) def_w_exam
from dictionary
where def not in ('', '+')
    and def not like '==%'
    and def not like '<=%'
    and def not like '=>%'
    and vocab not like '%...'
;

-- random word
select vocab word, def || def_w_exam def
from v_dictionary
offset random() * (select count(*) from v_dictionary)
limit 1;

-- search word, maximum 5 items
select vocab word
    , array_to_string(array_agg(def || def_w_exam),'\n') defs
from v_dictionary
where vocab ilike '%ящер%'
group by vocab
having count(*) <= 5;
