(set-logic ALL)
; Frontier Constraint ID: 7623583cc30db5ef
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1345)) (False)
(assert (not (= x 1345)))

; Query: ((== x 1346)) (False)
(assert (not (not (= x 1346))))

(check-sat)
(get-model)
