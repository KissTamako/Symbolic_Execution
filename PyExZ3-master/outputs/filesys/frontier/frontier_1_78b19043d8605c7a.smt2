(set-logic ALL)
; Frontier Constraint ID: 78b19043d8605c7a
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1312)) (False)
(assert (not (= x 1312)))

; Query: ((== x 1313)) (False)
(assert (not (not (= x 1313))))

(check-sat)
(get-model)
