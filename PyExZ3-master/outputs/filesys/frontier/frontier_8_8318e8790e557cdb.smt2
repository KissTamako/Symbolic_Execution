(set-logic ALL)
; Frontier Constraint ID: 8318e8790e557cdb
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 499)) (False)
(assert (not (not (= x 499))))

(check-sat)
(get-model)
