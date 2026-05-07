

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b10)
(ontable b4)
(on b5 b1)
(on b6 b7)
(on b7 b5)
(on b8 b4)
(on b9 b2)
(ontable b10)
(clear b6)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b2)
(on b5 b10)
(on b6 b1)
(on b7 b4)
(on b8 b9)
(on b10 b3))
)
)


