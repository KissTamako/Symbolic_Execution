(set-logic ALL)
; Constraint ID: 4a4f7a32b94ff9d9
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60082)) (False)
(assert (not (= x 60082)))

; Query: ((== x 60083)) (False)
(assert (not (not (= x 60083))))

(check-sat)
(get-model)
