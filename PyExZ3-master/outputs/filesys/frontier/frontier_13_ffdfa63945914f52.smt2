(set-logic ALL)
; Frontier Constraint ID: ffdfa63945914f52
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1705)) (False)
(assert (not (= x 1705)))

; Query: ((== x 1706)) (False)
(assert (not (not (= x 1706))))

(check-sat)
(get-model)
