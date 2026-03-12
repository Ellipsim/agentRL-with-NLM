

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on-table b3)
(on b4 b10)
(on b5 b6)
(on b6 b9)
(on-table b7)
(on-table b8)
(on-table b9)
(on-table b10)
(clear b1)
(clear b2)
(clear b3)
(clear b5)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b6)
(on b3 b8)
(on b4 b9)
(on b6 b10)
(on b7 b5)
(on b8 b2)
(on b9 b7)
(on b10 b4))
)
)


