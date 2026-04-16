(set-logic ALL)
; Constraint ID: 044b3a774d54604c
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59836)) (False)
(assert (not (= x 59836)))

; Query: ((== x 59837)) (False)
(assert (not (not (= x 59837))))

(check-sat)
(get-model)
