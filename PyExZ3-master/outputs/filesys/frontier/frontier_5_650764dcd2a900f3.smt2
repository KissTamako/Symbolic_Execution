(set-logic ALL)
; Constraint ID: 650764dcd2a900f3
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60667)) (False)
(assert (not (= x 60667)))

; Query: ((== x 60668)) (False)
(assert (not (not (= x 60668))))

(check-sat)
(get-model)
