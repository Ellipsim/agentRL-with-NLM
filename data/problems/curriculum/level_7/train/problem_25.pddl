

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b8)
(on-table b2)
(on-table b3)
(on b4 b6)
(on b5 b9)
(on b6 b1)
(on-table b7)
(on b8 b7)
(on-table b9)
(clear b2)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b2 b9)
(on b3 b1)
(on b4 b6)
(on b5 b2)
(on b6 b8)
(on b7 b5)
(on b8 b3))
)
)


