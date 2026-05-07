

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b7)
(ontable b2)
(ontable b3)
(on b4 b2)
(on b5 b1)
(on b6 b4)
(on b7 b10)
(ontable b8)
(on b9 b6)
(on b10 b9)
(clear b3)
(clear b5)
(clear b8)
)
(:goal
(and
(on b3 b6)
(on b4 b2)
(on b6 b1)
(on b8 b7)
(on b10 b5))
)
)


