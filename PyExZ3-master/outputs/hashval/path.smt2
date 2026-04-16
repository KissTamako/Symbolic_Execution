(set-logic ALL)
; Path ID: 76680e2b8cdc65fb
; Generated at: 2026-04-16 12:01:28
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const key Int)
(declare-const se Int)


; Query: ((== (^ (+ key (<< key 10)) (>> (+ key (<< key 10)) 6)) (+ key 1))) (False)
(assert (not (not (= ^ (+ key 1)))))

(check-sat)
(get-model)
