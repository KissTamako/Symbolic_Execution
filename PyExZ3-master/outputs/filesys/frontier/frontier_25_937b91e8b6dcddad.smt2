(set-logic ALL)
; Frontier Constraint ID: 937b91e8b6dcddad
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1048)) (False)
(assert (not (= x 1048)))

; Query: ((== x 1049)) (False)
(assert (not (not (= x 1049))))

(check-sat)
(get-model)
