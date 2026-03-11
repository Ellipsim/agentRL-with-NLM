

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b3)
(on b3 b1)
(on b4 b9)
(on b5 b7)
(on-table b6)
(on-table b7)
(on-table b8)
(on-table b9)
(clear b2)
(clear b5)
(clear b6)
(clear b8)
)
(:goal
(and
(on b2 b4)
(on b3 b5)
(on b5 b6)
(on b6 b1)
(on b7 b8)
(on b8 b3)
(on b9 b2))
)
)


