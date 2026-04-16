(set-logic ALL)
; Frontier Constraint ID: 2faf754d3359cb6d
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1621)) (False)
(assert (not (= x 1621)))

; Query: ((== x 1622)) (False)
(assert (not (not (= x 1622))))

(check-sat)
(get-model)
