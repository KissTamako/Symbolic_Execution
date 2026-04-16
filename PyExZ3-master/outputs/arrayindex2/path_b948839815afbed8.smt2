(set-logic ALL)
; Path ID: b948839815afbed8
; Generated at: 2026-04-16 12:01:19
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const i Int)
(declare-const se Int)

; ((== i 4)) (False)
(assert (not (= i 4)))
; ((== i 1)) (False)
(assert (not (= i 1)))

; Query: ((== i 6)) (True)
(assert (not (= i 6)))

(check-sat)
(get-model)
