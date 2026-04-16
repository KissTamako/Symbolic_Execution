(set-logic ALL)
; Frontier Constraint ID: db4d086237b0f697
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1642)) (False)
(assert (not (= x 1642)))

; Query: ((== x 1643)) (False)
(assert (not (not (= x 1643))))

(check-sat)
(get-model)
