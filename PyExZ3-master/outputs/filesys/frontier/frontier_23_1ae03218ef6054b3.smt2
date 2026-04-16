(set-logic ALL)
; Constraint ID: 1ae03218ef6054b3
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60619)) (False)
(assert (not (= x 60619)))

; Query: ((== x 60620)) (False)
(assert (not (not (= x 60620))))

(check-sat)
(get-model)
