(set-logic ALL)
; Constraint ID: 6548484ef19473a3
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59623)) (False)
(assert (not (= x 59623)))

; Query: ((== x 59624)) (False)
(assert (not (not (= x 59624))))

(check-sat)
(get-model)
