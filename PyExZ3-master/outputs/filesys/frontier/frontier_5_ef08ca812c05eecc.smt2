(set-logic ALL)
; Frontier Constraint ID: ef08ca812c05eecc
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1468)) (False)
(assert (not (= x 1468)))

; Query: ((== x 1469)) (False)
(assert (not (not (= x 1469))))

(check-sat)
(get-model)
