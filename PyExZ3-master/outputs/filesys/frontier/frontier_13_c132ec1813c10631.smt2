(set-logic ALL)
; Frontier Constraint ID: c132ec1813c10631
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2830)) (False)
(assert (not (= x 2830)))

; Query: ((== x 2831)) (False)
(assert (not (not (= x 2831))))

(check-sat)
(get-model)
