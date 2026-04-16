(set-logic ALL)
; Path ID: 2875d332c3e6ffcf
; Generated at: 2026-04-16 12:01:18
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const a Int)
(declare-const b Int)
(declare-const se Int)

; ((< a 0)) (True)
(assert (< a 0))

; Query: ((== (abs a) b)) (True)
(assert (not (= (abs a) b)))

(check-sat)
(get-model)
