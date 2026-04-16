(set-logic ALL)
; Path ID: 4ce0c4120462e7ac
; Generated at: 2026-04-16 12:01:29
; Solver: Z3Wrapper
; Number of assertions: 6
; Has query: True

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(declare-const d Int)
(declare-const se Int)

; ((< d c)) (False)
(assert (not (< d c)))
; ((< d b)) (False)
(assert (not (< d b)))
; ((< d a)) (False)
(assert (not (< d a)))
; ((< b d)) (True)
(assert (< b d))
; ((< c d)) (True)
(assert (< c d))
; ((< a b)) (True)
(assert (< a b))

; Query: ((< d d)) (False)
(assert (not (not (< d d))))

(check-sat)
(get-model)
