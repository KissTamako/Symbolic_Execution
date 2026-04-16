(set-logic ALL)
; Frontier Constraint ID: e27e89b4bf0cde4b
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1330)) (False)
(assert (not (not (= x 1330))))

(check-sat)
(get-model)
