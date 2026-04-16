(set-logic ALL)
; Frontier Constraint ID: d4e33a3289a95f25
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1861)) (False)
(assert (not (not (= x 1861))))

(check-sat)
(get-model)
