(set-logic ALL)
; Constraint ID: 08f55712ccc02da1
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60136)) (False)
(assert (not (= x 60136)))

; Query: ((== x 60137)) (False)
(assert (not (not (= x 60137))))

(check-sat)
(get-model)
