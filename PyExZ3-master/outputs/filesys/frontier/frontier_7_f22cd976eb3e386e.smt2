(set-logic ALL)
; Frontier Constraint ID: f22cd976eb3e386e
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1171)) (False)
(assert (not (= x 1171)))

; Query: ((== x 1172)) (False)
(assert (not (not (= x 1172))))

(check-sat)
(get-model)
