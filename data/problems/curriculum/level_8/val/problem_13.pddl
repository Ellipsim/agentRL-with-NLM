

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b2)
(on-table b4)
(on-table b5)
(on b6 b8)
(on-table b7)
(on b8 b5)
(on b9 b4)
(on b10 b9)
(clear b1)
(clear b3)
(clear b6)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b2 b10)
(on b3 b5)
(on b6 b7)
(on b7 b2)
(on b9 b8)
(on b10 b3))
)
)


