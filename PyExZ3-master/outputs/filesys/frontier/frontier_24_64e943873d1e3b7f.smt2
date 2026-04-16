(set-logic ALL)
; Frontier Constraint ID: 64e943873d1e3b7f
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2848)) (False)
(assert (not (not (= x 2848))))

(check-sat)
(get-model)
