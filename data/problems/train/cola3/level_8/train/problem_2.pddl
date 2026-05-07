

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b9)
(on b4 b5)
(on b5 b7)
(ontable b6)
(on b7 b10)
(ontable b8)
(ontable b9)
(on b10 b8)
(clear b1)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b8)
(on b4 b1)
(on b5 b2)
(on b6 b7)
(on b8 b5)
(on b9 b4))
)
)


