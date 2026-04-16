(set-logic ALL)
; Constraint ID: 2958fab30a953a06
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60682)) (False)
(assert (not (= x 60682)))

; Query: ((== x 60683)) (False)
(assert (not (not (= x 60683))))

(check-sat)
(get-model)
