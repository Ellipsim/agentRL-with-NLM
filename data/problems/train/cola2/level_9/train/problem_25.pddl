

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(on b3 b4)
(ontable b4)
(on b5 b8)
(on b6 b3)
(ontable b7)
(on b8 b10)
(ontable b9)
(on b10 b7)
(clear b1)
(clear b2)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b9)
(on b3 b4)
(on b4 b10)
(on b5 b2)
(on b6 b1)
(on b8 b3)
(on b9 b8)
(on b10 b7))
)
)


