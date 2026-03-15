

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(on b3 b9)
(on b4 b8)
(on-table b5)
(on b6 b1)
(on b7 b4)
(on b8 b5)
(on-table b9)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b3 b7)
(on b4 b3)
(on b6 b8)
(on b7 b2)
(on b8 b5)
(on b9 b1))
)
)


